import React, { useState, useEffect } from "react";
import styles from "./DataTransformationForm.module.scss";

const DataTransformationForm = ({ onSubmit, onClose }) => {
    const [contracts, setContracts] = useState([]);
    const [name, setName] = useState(""); // Название трансформатора
    const [selectedContract, setSelectedContract] = useState("");
    const [selectedLanguage, setSelectedLanguage] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        // Загрузка списка контрактов из API
        const fetchContracts = async () => {
            try {
                const response = await fetch("http://localhost:8002/contracts");
                if (response.ok) {
                    const data = await response.json();
                    setContracts(data);
                } else {
                    console.error("Ошибка загрузки контрактов");
                }
            } catch (error) {
                console.error("Ошибка подключения к API", error);
            }
        };

        fetchContracts();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        const newTransformation = {
            name,
            contract: selectedContract,
            language: selectedLanguage,
        };

        // Имитация отправки на сервер
        try {
            // Здесь можно добавить POST-запрос на создание нового трансформатора
            onSubmit(newTransformation);
        } catch (error) {
            console.error("Ошибка при создании трансформатора", error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className={styles.formContainer}>
            <form className={styles.form} onSubmit={handleSubmit}>
                <h2>Добавить трансформатор</h2>
                <label>
                    Название трансформатора:
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Введите название"
                        required
                    />
                </label>
                <label>
                    Выберите контракт:
                    <select
                        value={selectedContract}
                        onChange={(e) => setSelectedContract(e.target.value)}
                        required
                    >
                        <option value="">Выберите контракт</option>
                        {contracts.map((contract) => (
                            <option key={contract.id} value={contract.id}>
                                {contract.name}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Выберите язык:
                    <select
                        value={selectedLanguage}
                        onChange={(e) => setSelectedLanguage(e.target.value)}
                        required
                    >
                        <option value="">Выберите язык</option>
                        <option value="Python">Python</option>
                        <option value="Java">Java</option>
                        <option value="Go">Go</option>
                        <option value="Groovy">Groovy</option>
                    </select>
                </label>
                <div className={styles.buttons}>
                    <button type="submit" disabled={isSubmitting}>
                        {isSubmitting ? "Создание..." : "Создать"}
                    </button>
                    <button type="button" onClick={onClose}>
                        Отмена
                    </button>
                </div>
            </form>
        </div>
    );
};

export default DataTransformationForm;
