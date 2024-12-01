import React from 'react';
import styles from './Navbar.module.scss';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
    const menuItems = [
        { name: 'Контракты', path: '/contracts' },
        {name: 'Конструктор Контрактов', path: '/contract-constructor'},
        { name: 'Источники Данных', path: '/data-sources' },
        { name: 'Трансформаторы Данных', path: '/transformers' },
        { name: 'Модели', path: '/models' },
        { name: 'Мониторинг', path: '/monitoring' },
        { name: 'Логгирование', path: '/logging' },
        { name: 'Справочник', path: '/documentation' },
    ];

    return (
        <nav className={styles.navbar}>
            <ul>
                {menuItems.map((item) => (
                    <li key={item.name}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) =>
                                isActive ? styles.activeLink : styles.link
                            }
                        >
                            {item.name}
                        </NavLink>
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default Navbar;
