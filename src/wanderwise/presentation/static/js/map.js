// Map configuration and functionality for WanderWise

class ItineraryMap {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container element with ID '${containerId}' not found`);
            return;
        }

        // Default options
        this.options = {
            mapboxToken: this.container.dataset.mapboxToken || '',
            center: [0, 0],
            zoom: 12,
            style: 'mapbox://styles/mapbox/streets-v12',
            ...options
        };

        this.map = null;
        this.markers = [];
        this.routes = [];

        this.init();
    }

    async init() {
        if (!this.options.mapboxToken) {
            console.error('Mapbox access token is required');
            return;
        }

        // Load Mapbox GL JS dynamically
        await this.loadMapbox();
        
        // Initialize the map
        this.map = new mapboxgl.Map({
            container: this.container.id,
            style: this.options.style,
            center: this.options.center,
            zoom: this.options.zoom,
            accessToken: this.options.mapboxToken
        });

        // Add navigation control
        this.map.addControl(new mapboxgl.NavigationControl());
        
        // Add geolocation control
        this.map.addControl(
            new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true,
                showUserHeading: true
            })
        );

        // Initialize map events
        this.setupEventListeners();
    }

    async loadMapbox() {
        return new Promise((resolve) => {
            if (window.mapboxgl) {
                resolve();
                return;
            }

            // Load Mapbox GL JS CSS
            const cssLink = document.createElement('link');
            cssLink.href = 'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css';
            cssLink.rel = 'stylesheet';
            document.head.appendChild(cssLink);

            // Load Mapbox GL JS
            const script = document.createElement('script');
            script.src = 'https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js';
            script.onload = () => {
                mapboxgl.accessToken = this.options.mapboxToken;
                resolve();
            };
            document.head.appendChild(script);
        });
    }

    setupEventListeners() {
        // Add click event to add new waypoints
        this.map.on('click', (e) => this.handleMapClick(e));
        
        // Handle map load
        this.map.on('load', () => {
            this.container.dispatchEvent(new Event('map:loaded'));
        });
    }

    handleMapClick(e) {
        // Emit custom event with clicked coordinates
        const event = new CustomEvent('map:click', {
            detail: {
                lngLat: e.lngLat,
                point: e.point
            }
        });
        this.container.dispatchEvent(event);
    }

    addMarker(coordinates, options = {}) {
        if (!this.map) return null;

        const marker = new mapboxgl.Marker({
            draggable: options.draggable || false,
            ...options
        })
            .setLngLat(coordinates)
            .addTo(this.map);

        if (options.draggable) {
            marker.on('dragend', () => {
                const lngLat = marker.getLngLat();
                this.container.dispatchEvent(new CustomEvent('marker:dragend', {
                    detail: { marker, lngLat }
                }));
            });
        }

        this.markers.push(marker);
        return marker;
    }

    addRoute(coordinates, options = {}) {
        if (!this.map) return null;

        const routeId = `route-${this.routes.length}`;
        const sourceId = `${routeId}-source`;
        const layerId = `${routeId}-layer`;

        this.map.addSource(sourceId, {
            type: 'geojson',
            data: {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: coordinates
                }
            }
        });

        this.map.addLayer({
            id: layerId,
            type: 'line',
            source: sourceId,
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': options.color || '#3b82f6',
                'line-width': 3,
                'line-opacity': 0.7
            }
        });

        this.routes.push({ id: routeId, sourceId, layerId });
        return routeId;
    }

    fitBounds(coordinates, padding = 100) {
        if (!this.map || !coordinates.length) return;

        const bounds = coordinates.reduce((bounds, coord) => {
            return bounds.extend(coord);
        }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));

        this.map.fitBounds(bounds, {
            padding: padding,
            maxZoom: 15
        });
    }

    clearMarkers() {
        this.markers.forEach(marker => marker.remove());
        this.markers = [];
    }

    clearRoutes() {
        this.routes.forEach(route => {
            if (this.map.getLayer(route.layerId)) {
                this.map.removeLayer(route.layerId);
            }
            if (this.map.getSource(route.sourceId)) {
                this.map.removeSource(route.sourceId);
            }
        });
        this.routes = [];
    }

    destroy() {
        if (this.map) {
            this.clearMarkers();
            this.clearRoutes();
            this.map.remove();
            this.map = null;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = { ItineraryMap };
} else {
    window.ItineraryMap = ItineraryMap;
}
