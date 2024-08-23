      document.addEventListener('DOMContentLoaded', function () {
          var toastElement = document.getElementById('registerToast');
          if (toastElement) {
              var toast = new bootstrap.Toast(toastElement, {
                  animation: true,
                  autohide: true,
                  delay: 4000
              });
              toast.show();
          }
      });