import React, { useState } from "react";
import styles from "./ContractsRegexForm.module.scss";

const ContractsRegexForm = ({ onSubmit, onClose }) => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [file, setFile] = useState(null);
    const [data, setData] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFile(file);

        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                try {
                    const parsedData = JSON.parse(reader.result);
                    setData(parsedData); // Сохраняем данные из JSON
                } catch (error) {
                    console.error("Invalid JSON file");
                }
            };
            reader.readAsText(file);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name || !description || !data) return;

        const newContract = {
            name,
            description,
            data, // Отправляем содержимое JSON как data
        };

        onSubmit(newContract);
        setName("");
        setDescription("");
        setFile(null);
        setData(null);
        onClose();
    };

    return (
        <div className={styles.formContainer}>
            <h2>Добавить контракт</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Название"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Описание"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <input type="file" accept=".json" onChange={handleFileChange} /> <br />
                <button type="submit">Добавить</button>
            </form>
        </div>
    );
};

export default ContractsRegexForm;
