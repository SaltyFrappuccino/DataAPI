import React from "react";
import styles from "./DataSource.module.scss";

const DataSource = ({ source }) => {
    const getStatusColor = (status) => {
        switch (status) {
            case "Активный":
                return styles.active;
            case "Ожидание":
                return styles.pending;
            case "Неактивный":
                return styles.inactive;
            case "Ошибка":
                return styles.error;
            default:
                source.status = "Неактивный";
                return styles.inactive;
        }
    };

    return (
        <div className={styles.row}>
            <span>{source.name}</span>
            <span>{source.db_type}</span>
            <span>
        <button className={`${styles.statusButton} ${getStatusColor(source.status)}`}>
          {source.status}
        </button>
      </span>
        </div>
    );
};

export default DataSource;
