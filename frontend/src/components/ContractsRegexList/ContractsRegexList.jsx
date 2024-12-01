import React from "react";
import Contract from "../Contract/Contract";
import styles from "./ContractsRegexList.module.scss";

const ContractsRegexList = ({ contracts }) => {
    return (
        <div className={styles.list}>
            <div className={styles.headerRow}>
                <span>Название</span>
                <span>Название модели</span>
                <span></span>
            </div>
            {contracts.map((contract) => (
                <Contract key={contract.id} data={contract} />
            ))}
        </div>
    );
};

export default ContractsRegexList;
