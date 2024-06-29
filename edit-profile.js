document.addEventListener('DOMContentLoaded', function() {
    const labels = document.querySelectorAll('.input-label');
    const inputs = document.querySelectorAll('.input-field');

    labels.forEach(label => {
      label.addEventListener('click', function() {
        const input = document.getElementById(label.htmlFor);
        input.focus();
        label.style.display = 'none';
      });
    });

    inputs.forEach(input => {
      input.addEventListener('blur', function() {
        if (input.value.trim() === '') {
          const label = document.querySelector(`label[for=${input.id}]`);
          label.style.display = 'block';
        }
      });
    });
});

function saveProfile() {
    const firstName = document.getElementById('first-name').value;
    const contactNumber = document.getElementById('contact-number').value;
    const lastName = document.getElementById('last-name').value;
    const dob = document.getElementById('dob').value;

    if (!firstName || !contactNumber || !lastName || !dob) {
        alert('Please fill in all the fields.');
        return;
    }

    const profileData = {
        firstName: firstName,
        contactNumber: contactNumber,
        lastName: lastName,
        dob: dob
    };

    fetch('your-backend-api-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(profileData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Profile updated successfully!');
            window.location.href = 'profile_view.html';
        } else {
            alert('Failed to update profile.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the profile.');
    });
}
