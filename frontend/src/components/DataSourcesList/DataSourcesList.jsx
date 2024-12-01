import React from 'react';
import styles from './DataSourcesList.module.scss';
import DataSource from '../DataSource/DataSource';

const DataSourcesList = ({ dataSources }) => {
    return (
        <div className={styles.list}>
            <div className={styles.headerRow}>
                <span>Название</span>
                <span>Тип источника</span>
                <span>Статус</span>
            </div>
            {dataSources.map((source) => (
                <DataSource key={source.id} source={source} />
            ))}
        </div>
    );
};

export default DataSourcesList;
