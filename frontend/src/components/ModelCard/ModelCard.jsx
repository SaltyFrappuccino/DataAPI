import React from "react";
import styles from "./ModelCard.module.scss";

const ModelCard = ({ model }) => {
    return (
        <div className={styles.card}>
            <img src={model.image} alt={model.name} className={styles.cover} />
            <div className={styles.info}>
                <h3 className={styles.name}>{model.name}</h3>
                <p className={styles.description}>{model.description}</p>
                <div className={styles.meta}>
                    <span className={styles.versionLabel}>Версия:</span>
                    <span className={styles.version}>{model.version}</span>
                </div>
            </div>
        </div>
    );
};

export default ModelCard;
