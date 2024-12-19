// Получение элементов
const menuButton = document.querySelector('.menu-button');
const dropdownMenu = document.querySelector('.dropdown');
let flag = false;

// Добавляем обработчик события для кнопки
menuButton.addEventListener('click', () => {
    flag = !flag
    // Переключение видимости меню
    if (flag) {
        dropdownMenu.style.display = 'block';
    } else {
        dropdownMenu.style.display = 'none';
    }
});

// Закрытие меню при клике вне его области
document.addEventListener('click', (event) => {
    // Проверяем, был ли клик за пределами меню и кнопки
    if (!menuButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.style.display = 'none';
        flag = !flag
    }
});
