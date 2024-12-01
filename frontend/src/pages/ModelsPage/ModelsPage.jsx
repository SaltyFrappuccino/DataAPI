import React, { useState } from "react";
import styles from "./ModelsPage.module.scss";
import ModelsList from "../../components/ModelsList/ModelsList";
import ModalForm from "../../components/ModalForm/ModalForm";
import ModelsForm from "../../components/ModelsForm/ModelsForm";

const ModelsPage = () => {
    const [search, setSearch] = useState("");
    const [models, setModels] = useState([
        { id: 1, name: "Модель 1", settings: "Default Settings", version: "1.0", image: "https://via.placeholder.com/710x295" },
        { id: 2, name: "Модель 2", settings: "Custom Settings", version: "2.0", image: "https://via.placeholder.com/710x295" },
        { id: 3, name: "Модель 3", settings: "Optimized Settings", version: "1.5", image: "https://via.placeholder.com/710x295" },
        { id: 4, name: "Модель 4", settings: "Experimental Settings", version: "1.1", image: "https://via.placeholder.com/710x295" },
        { id: 5, name: "Модель 5", settings: "Advanced Settings", version: "3.0", image: "https://via.placeholder.com/710x295" },
    ]);
    const [isModalOpen, setModalOpen] = useState(false);

    const filteredModels = models.filter((model) =>
        model.name.toLowerCase().includes(search.toLowerCase())
    );

    const handleAddModel = (newModel) => {
        setModels([...models, newModel]);
        setModalOpen(false); // Закрыть модальное окно после добавления
    };

    return (
        <div className={styles.container}>
            <h1>Модели</h1>
            <div className={styles.searchRow}>
                <input
                    type="text"
                    placeholder="Поиск"
                    className={styles.searchInput}
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
                <button
                    className={styles.addButton}
                    onClick={() => setModalOpen(true)}
                >
                    Добавить модель
                </button>
            </div>
            <ModelsList models={filteredModels} />
            <ModalForm isOpen={isModalOpen} onClose={() => setModalOpen(false)}>
                <ModelsForm onSubmit={handleAddModel} />
            </ModalForm>
        </div>
    );
};

export default ModelsPage;
