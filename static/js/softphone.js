document.getElementById('openSidebar').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('sidebar-open');
    sidebar.classList.toggle('sidebar-closed');
    const content = document.getElementById('sidebarContent');
    if (sidebar.classList.contains('sidebar-open')) {
        content.classList.remove('hidden-scroll');
    } else {
        setTimeout(() => content.classList.add('hidden-scroll'), 300); // Esperar animação da sidebar
    }
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

