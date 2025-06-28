// Resume Portfolio Builder JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form functionality
    initializeSkillsInput();
    initializeFormValidation();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// Skills management
let skills = [];

function initializeSkillsInput() {
    const skillsInput = document.getElementById('skills-input');
    if (skillsInput) {
        skillsInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addSkill();
            }
        });
    }
}

function addSkill() {
    const skillsInput = document.getElementById('skills-input');
    const skill = skillsInput.value.trim();
    
    if (skill && !skills.includes(skill)) {
        skills.push(skill);
        updateSkillsDisplay();
        skillsInput.value = '';
    } else if (skills.includes(skill)) {
        showAlert('This skill is already added!', 'warning');
    }
}

function removeSkill(skillToRemove) {
    skills = skills.filter(skill => skill !== skillToRemove);
    updateSkillsDisplay();
}

function updateSkillsDisplay() {
    const container = document.getElementById('skills-container');
    container.innerHTML = '';
    
    skills.forEach(skill => {
        const skillElement = document.createElement('div');
        skillElement.className = 'skill-item';
        skillElement.innerHTML = `
            ${skill}
            <button type="button" class="skill-remove" onclick="removeSkill('${skill}')" title="Remove skill">
                <i class="fas fa-times"></i>
            </button>
            <input type="hidden" name="skills" value="${skill}">
        `;
        container.appendChild(skillElement);
    });
}

// Dynamic form sections
function addEducation() {
    const container = document.getElementById('education-container');
    const educationItem = document.createElement('div');
    educationItem.className = 'education-item';
    educationItem.innerHTML = `
        <div class="row">
            <div class="col-md-4 mb-3">
                <label class="form-label">School/University</label>
                <input type="text" class="form-control" name="education_school" placeholder="University Name">
            </div>
            <div class="col-md-4 mb-3">
                <label class="form-label">Degree</label>
                <input type="text" class="form-control" name="education_degree" placeholder="Bachelor of Science">
            </div>
            <div class="col-md-3 mb-3">
                <label class="form-label">Year</label>
                <input type="text" class="form-control" name="education_year" placeholder="2020-2024">
            </div>
            <div class="col-md-1 mb-3 d-flex align-items-end">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeEducation(this)" title="Remove">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(educationItem);
    
    // Add animation
    educationItem.style.opacity = '0';
    educationItem.style.transform = 'translateY(20px)';
    setTimeout(() => {
        educationItem.style.transition = 'all 0.3s ease';
        educationItem.style.opacity = '1';
        educationItem.style.transform = 'translateY(0)';
    }, 10);
}

function removeEducation(button) {
    const educationItem = button.closest('.education-item');
    if (document.querySelectorAll('.education-item').length > 1) {
        educationItem.style.transition = 'all 0.3s ease';
        educationItem.style.opacity = '0';
        educationItem.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            educationItem.remove();
        }, 300);
    } else {
        showAlert('You must have at least one education entry!', 'warning');
    }
}

function addExperience() {
    const container = document.getElementById('experience-container');
    const experienceItem = document.createElement('div');
    experienceItem.className = 'experience-item';
    experienceItem.innerHTML = `
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Company</label>
                <input type="text" class="form-control" name="experience_company" placeholder="Company Name">
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Position</label>
                <input type="text" class="form-control" name="experience_position" placeholder="Job Title">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Period</label>
                <input type="text" class="form-control" name="experience_period" placeholder="Jan 2020 - Present">
            </div>
            <div class="col-md-5 mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" name="experience_description" rows="2" placeholder="Describe your role and achievements..."></textarea>
            </div>
            <div class="col-md-1 mb-3 d-flex align-items-end">
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeExperience(this)" title="Remove">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(experienceItem);
    
    // Add animation
    experienceItem.style.opacity = '0';
    experienceItem.style.transform = 'translateY(20px)';
    setTimeout(() => {
        experienceItem.style.transition = 'all 0.3s ease';
        experienceItem.style.opacity = '1';
        experienceItem.style.transform = 'translateY(0)';
    }, 10);
}

function removeExperience(button) {
    const experienceItem = button.closest('.experience-item');
    if (document.querySelectorAll('.experience-item').length > 1) {
        experienceItem.style.transition = 'all 0.3s ease';
        experienceItem.style.opacity = '0';
        experienceItem.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            experienceItem.remove();
        }, 300);
    } else {
        showAlert('You must have at least one experience entry!', 'warning');
    }
}

// Form validation
function initializeFormValidation() {
    const form = document.getElementById('portfolioForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            } else {
                // Show loading state
                const submitButton = form.querySelector('button[type="submit"]');
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitButton.disabled = true;
                
                // Re-enable after timeout (in case of error)
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 5000);
            }
        });
    }
}

function validateForm() {
    const name = document.getElementById('name').value.trim();
    const jobTitle = document.getElementById('job_title').value.trim();
    
    if (!name) {
        showAlert('Please enter your full name', 'danger');
        document.getElementById('name').focus();
        return false;
    }
    
    if (!jobTitle) {
        showAlert('Please enter your job title', 'danger');
        document.getElementById('job_title').focus();
        return false;
    }
    
    // Validate file upload
    const photoInput = document.getElementById('photo');
    if (photoInput.files.length > 0) {
        const file = photoInput.files[0];
        const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif'];
        const maxSize = 16 * 1024 * 1024; // 16MB
        
        if (!allowedTypes.includes(file.type)) {
            showAlert('Please upload a valid image file (PNG, JPG, JPEG, GIF)', 'danger');
            return false;
        }
        
        if (file.size > maxSize) {
            showAlert('Image file size must be less than 16MB', 'danger');
            return false;
        }
    }
    
    return true;
}

// Utility functions
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    const container = main.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
    
    // Scroll to alert
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// File upload preview
document.addEventListener('change', function(e) {
    if (e.target.id === 'photo') {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // You could add a preview here if needed
                console.log('Photo selected:', file.name);
            };
            reader.readAsDataURL(file);
        }
    }
});

// Smooth transitions for form sections
function animateSection(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'all 0.5s ease';
    
    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

// Initialize animations when page loads
window.addEventListener('load', function() {
    const sections = document.querySelectorAll('.section-card');
    sections.forEach((section, index) => {
        setTimeout(() => {
            animateSection(section);
        }, index * 100);
    });
});

// Auto-save to localStorage (optional feature)
function autoSave() {
    const formData = new FormData(document.getElementById('portfolioForm'));
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (data[key]) {
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    // Add skills
    data['skills'] = skills;
    
    localStorage.setItem('portfolioFormData', JSON.stringify(data));
}

// Load saved data (optional feature)
function loadSavedData() {
    const savedData = localStorage.getItem('portfolioFormData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            // You could implement loading saved data here
            console.log('Saved data available:', data);
        } catch (e) {
            console.error('Error loading saved data:', e);
        }
    }
}

// Export functionality helpers
function downloadPortfolio() {
    // This function is called from the template
    // The actual export is handled by the Flask backend
    showAlert('Preparing your portfolio for download...', 'info');
}
