import React, { useState, useEffect } from "react";
import styles from "./DataSourcesPage.module.scss";
import DataSourcesList from "../../components/DataSourcesList/DataSourcesList";
import ModalForm from "../../components/ModalForm/ModalForm";
import DataSourceForm from "../../components/DataSourceForm/DataSourceForm";

const DataSourcesPage = () => {
    const [search, setSearch] = useState("");
    const [dataSources, setDataSources] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);

    // Fetch data sources from the API
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8002/db_connections");
                const data = await response.json();
                setDataSources(data);
            } catch (error) {
                console.error("Error fetching data sources", error);
            }
        };

        fetchData();
    }, []);

    const filteredSources = dataSources.filter((source) =>
        source.name.toLowerCase().includes(search.toLowerCase())
    );

    const handleAddSource = (newSource) => {
        setDataSources((prevSources) => [...prevSources, newSource]);
    };

    return (
        <div className={styles.container}>
            <h1>Источники данных</h1>
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
                    Добавить источник
                </button>
            </div>
            <DataSourcesList dataSources={filteredSources} />
            <ModalForm isOpen={isModalOpen} onClose={() => setModalOpen(false)}>
                <DataSourceForm onSubmit={handleAddSource} />
            </ModalForm>
        </div>
    );
};

export default DataSourcesPage;
