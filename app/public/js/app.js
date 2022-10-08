let getstarted = document.getElementById('getStarted');

getstarted.onclick = () => {
    Swal.fire({
        title: 'საშუალო ფასი',
        text: 'ჩვენი ჭკვიანი ალგორითმის საშუალებით შეგიძლიათ გაიგოთ ამათუიმ ავტომობილის საბაზრო ფასის საშუალო არითმეტიკული შეიყვანეთ მანქანის სახელი და მიიღეთ საშუალო ფასი',
        input: 'text',
        inputAttributes: {
            autocapitalize: 'off',
            placeholder: 'ავტომობილის სახელი'
        },
        showCancelButton: true,
        cancelButtonText: 'გაუქმება',
        confirmButtonText: 'პროგნოზირება',
        showLoaderOnConfirm: true,

        preConfirm: (car_name) => {
            return fetch(`/api/v1/predict-price?car=${car_name}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(response.statusText)
                    }

                    return response.json();
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `მოხდა შეცდომა: ${error}`
                    );
                });
            },

        allowOutsideClick: () => !Swal.isLoading()

    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: result.value.message,
                confirmButtonText: 'გასაგებია'
            });
        }
    })
}