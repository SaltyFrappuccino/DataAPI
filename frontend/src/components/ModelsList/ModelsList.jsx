import React from "react";
import styles from "./ModelsList.module.scss";

const ModelsList = ({ models }) => {
    if (models.length === 0) {
        return <p>Модели не найдены.</p>;
    }

    return (
        <ul className={styles.list}>
            {models.map((model) => (
                <li key={model.id} className={styles.item}>
                    <img src={model.image} alt={model.name} className={styles.image} />
                    <div className={styles.details}>
                        <h3>{model.name}</h3>
                        <p>Версия: {model.version}</p>
                        <p>{model.settings}</p>
                    </div>
                </li>
            ))}
        </ul>
    );
};

export default ModelsList;
