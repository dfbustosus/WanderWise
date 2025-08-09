/**
 * Drag and Drop functionality for WanderWise itinerary activities
 * 
 * This script enables users to reorder activities within their daily plans
 * using a drag-and-drop interface.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize drag and drop for all activity lists
    initDragAndDrop();
    
    // Listen for HTMX content swaps to reinitialize drag and drop
    document.body.addEventListener('htmx:afterSwap', function() {
        initDragAndDrop();
    });
});

/**
 * Initialize drag and drop functionality for all activity lists
 */
function initDragAndDrop() {
    const activityLists = document.querySelectorAll('.activity-list');
    
    activityLists.forEach(list => {
        // Make sure we don't add multiple event listeners
        if (list.dataset.dragInitialized) return;
        list.dataset.dragInitialized = 'true';
        
        // Add drag and drop event listeners
        list.addEventListener('dragover', handleDragOver);
        list.addEventListener('dragenter', handleDragEnter);
        list.addEventListener('dragleave', handleDragLeave);
        list.addEventListener('drop', handleDrop);
        list.addEventListener('dragend', handleDragEnd);
        
        // Make all activities draggable
        const activities = list.querySelectorAll('.activity-item');
        activities.forEach(activity => {
            activity.draggable = true;
            activity.addEventListener('dragstart', handleDragStart);
            
            // Add drag handle if not already present
            if (!activity.querySelector('.drag-handle')) {
                const dragHandle = document.createElement('span');
                dragHandle.className = 'drag-handle';
                dragHandle.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                `;
                activity.insertBefore(dragHandle, activity.firstChild);
            }
        });
    });
}

// Global variables to track drag state
let draggedItem = null;
let dragOverItem = null;

function handleDragStart(e) {
    draggedItem = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
    
    // Set a custom drag image (optional)
    const dragIcon = document.createElement('div');
    dragIcon.innerHTML = this.querySelector('.drag-handle').outerHTML;
    document.body.appendChild(dragIcon);
    e.dataTransfer.setDragImage(dragIcon, 10, 10);
    setTimeout(() => document.body.removeChild(dragIcon), 0);
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    e.preventDefault();
    this.classList.add('drag-over');
    
    // Find the closest activity item or use the list
    const targetItem = e.target.closest('.activity-item');
    if (targetItem && targetItem !== draggedItem) {
        dragOverItem = targetItem;
        const rect = targetItem.getBoundingClientRect();
        const midpoint = rect.top + (rect.height / 2);
        
        if (e.clientY > midpoint) {
            // Insert after
            targetItem.classList.remove('drag-over-above');
            targetItem.classList.add('drag-over-below');
        } else {
            // Insert before
            targetItem.classList.remove('drag-over-below');
            targetItem.classList.add('drag-over-above');
        }
    }
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
    const targetItem = e.target.closest('.activity-item');
    if (targetItem) {
        targetItem.classList.remove('drag-over-above', 'drag-over-below');
    }
}

function handleDrop(e) {
    e.stopPropagation();
    e.preventDefault();
    
    if (dragOverItem && dragOverItem !== draggedItem) {
        const rect = dragOverItem.getBoundingClientRect();
        const midpoint = rect.top + (rect.height / 2);
        
        if (e.clientY > midpoint) {
            // Insert after
            dragOverItem.parentNode.insertBefore(draggedItem, dragOverItem.nextSibling);
        } else {
            // Insert before
            dragOverItem.parentNode.insertBefore(draggedItem, dragOverItem);
        }
    }
    
    // Clean up
    this.classList.remove('drag-over');
    const items = this.querySelectorAll('.activity-item');
    items.forEach(item => {
        item.classList.remove('drag-over-above', 'drag-over-below');
    });
    
    // Update the order in the backend
    updateActivityOrder(this);
    
    return false;
}

function handleDragEnd() {
    this.classList.remove('dragging');
    draggedItem = null;
    dragOverItem = null;
}

/**
 * Update the activity order in the backend
 * @param {HTMLElement} listElement - The activity list element
 */
function updateActivityOrder(listElement) {
    const dayId = listElement.closest('.day-plan').dataset.dayId;
    const activityItems = listElement.querySelectorAll('.activity-item');
    const order = Array.from(activityItems).map(item => item.dataset.activityId);
    
    // Send the new order to the server
    fetch('/api/itinerary/reorder-activities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // If using CSRF protection
        },
        body: JSON.stringify({
            day_id: dayId,
            activity_order: order
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update activity order');
        }
        return response.json();
    })
    .then(data => {
        console.log('Activity order updated:', data);
        // Optionally show a success message
        showNotification('Itinerary updated successfully', 'success');
    })
    .catch(error => {
        console.error('Error updating activity order:', error);
        // Optionally show an error message
        showNotification('Failed to update activity order', 'error');
    });
}

/**
 * Helper function to get a cookie value by name
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

/**
 * Show a notification to the user
 */
function showNotification(message, type = 'info') {
    // Implementation depends on your notification system
    // This is a simple example using alert
    alert(message);
}
