import React, { useState, useEffect } from "react";
import styles from "./ContractsRegexPage.module.scss";
import ContractsRegexList from "../../components/ContractsRegexList/ContractsRegexList";
import ModalForm from "../../components/ModalForm/ModalForm";
import ContractsRegexForm from "../../components/ContractsRegexForm/ContractsRegexForm";

const ContractsRegexPage = () => {
    const [search, setSearch] = useState("");
    const [contracts, setContracts] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);

    // Загружаем контракты с API
    useEffect(() => {
        const fetchContracts = async () => {
            const response = await fetch("http://localhost:8002/contracts");
            const data = await response.json();
            setContracts(data);
        };
        fetchContracts();
    }, []);

    const filteredContracts = contracts.filter((contract) =>
        contract.name.toLowerCase().includes(search.toLowerCase())
    );

    const handleAddContract = async (newContract) => {
        const response = await fetch("http://localhost:8002/contracts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(newContract),
        });

        if (response.ok) {
            const data = await response.json();
            setContracts([...contracts, data]);
        } else {
            console.error("Failed to add contract");
        }
    };

    return (
        <div className={styles.container}>
            <h1>Контракты (Regex)</h1>
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
                    Добавить контракт
                </button>
            </div>
            <ContractsRegexList contracts={filteredContracts} />
            <ModalForm isOpen={isModalOpen} onClose={() => setModalOpen(false)}>
                <ContractsRegexForm onSubmit={handleAddContract} onClose={() => setModalOpen(false)} />
            </ModalForm>
        </div>
    );
};

export default ContractsRegexPage;
