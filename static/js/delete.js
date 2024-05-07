const btnBorrar = document.querySelectorAll('.btn-borrar');

if (btnBorrar) {
    const btnArray = Array.from(btnBorrar);
    btnArray.forEach((btn) => {
        // <-- Agrega paréntesis aquí
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Estás seguro de eliminar el administrador?')) {
                e.preventDefault();
            }
        });
    });
}