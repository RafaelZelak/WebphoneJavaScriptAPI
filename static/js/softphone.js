document.getElementById('openSidebar').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('sidebar-open');
    sidebar.classList.toggle('sidebar-closed');
    const content = document.getElementById('sidebarContent');
    const listicon = document.getElementById('list-icon');

    if (sidebar.classList.contains('sidebar-open')) {
        content.classList.remove('hidden-scroll');
        if (listicon) {
            listicon.src = 'static/img/listActive.svg'; // Troca para o ícone ativo
        }
    } else {
        setTimeout(() => content.classList.add('hidden-scroll'), 300); // Esperar animação da sidebar
        if (listicon) {
            listicon.src = 'static/img/list.svg'; // Troca para o ícone desativado
        }
    }k
});

document.getElementById('searchBox').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const items = document.querySelectorAll('.caller-item');

    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(filter)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});
