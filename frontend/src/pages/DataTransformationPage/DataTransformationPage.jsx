import React, { useState, useEffect } from "react";
import styles from "./DataTransformationPage.module.scss";
import DataTransformationList from "../../components/DataTransformationList/DataTransformationList";
import DataTransformationForm from "../../components/DataTransformationForm/DataTransformationForm";

const DataTransformationPage = () => {
    const [transformations, setTransformations] = useState([]);
    const [isFormVisible, setIsFormVisible] = useState(false);

    useEffect(() => {
        // Загрузка списка трансформаторов из API
        const fetchTransformations = async () => {
            try {
                const response = await fetch("http://localhost:8002/data_transformation_instruction");
                if (response.ok) {
                    const data = await response.json();
                    setTransformations(data);
                } else {
                    console.error("Ошибка загрузки трансформаторов");
                }
            } catch (error) {
                console.error("Ошибка подключения к API", error);
            }
        };

        fetchTransformations();
    }, []);

    const handleAddClick = () => {
        setIsFormVisible(true);
    };

    const handleFormSubmit = (newTransformation) => {
        setTransformations((prev) => [...prev, newTransformation]);
        setIsFormVisible(false);
    };

    return (
        <div className={styles.container}>
            <h1>Трансформаторы данных</h1>
            <div className={styles.searchRow}>
                <input type="text" placeholder="Поиск" className={styles.searchInput} />
                <button className={styles.addButton} onClick={handleAddClick}>
                    Добавить трансформатор
                </button>
            </div>
            <DataTransformationList transformations={transformations} />
            {isFormVisible && <DataTransformationForm onSubmit={handleFormSubmit} onClose={() => setIsFormVisible(false)} />}
        </div>
    );
};

export default DataTransformationPage;
