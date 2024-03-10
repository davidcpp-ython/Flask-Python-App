function deletePatient(patientId) {
    fetch('/delete-patient', {
        method: 'POST',
        body: JSON.stringify({ patientId: patientId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}