import React from "react";
import styles from "./Contract.module.scss";

const Contract = ({ data }) => {

    return (
        <div className={styles.row}>
            <span>{data.name}</span>
            <span>{data.data.model.name}</span>
            <button className={styles.editButton}>Редактировать</button>
        </div>
    );
};

export default Contract;
