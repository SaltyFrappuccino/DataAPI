import React from "react";
import DataTransformation from "../DataTransformation/DataTransformation";
import styles from "./DataTransformationList.module.scss";

const DataTransformationList = ({ transformations }) => {
    return (
        <div className={styles.list}>
            <div className={styles.headerRow}>
                <span>Название</span>
                <span>Название модели</span>
                <span>Язык трансформатора</span>
                <span></span>
            </div>
            {transformations.map((transformation) => (
                <DataTransformation key={transformation.id} data={transformation} />
            ))}
        </div>
    );
};

export default DataTransformationList;
