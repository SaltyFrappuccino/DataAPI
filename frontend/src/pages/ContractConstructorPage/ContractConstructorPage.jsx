import React, { useState } from "react";
import styles from "./ContractConstructorPage.module.scss";

const ContractConstructor = () => {
    const [contractData, setContractData] = useState({
        contract_id: "",
        name: "",
        description: "",
        model: {
            id: "",
            name: "",
            version: "",
        },
        fields: [
            {
                name: "",
                type: "",
                source: {
                    id: "",
                    name: "",
                    field_mapping: {
                        source_field: "",
                        target_field: "",
                    },
                    authentication: {
                        type: "",
                        credentials: {
                            username: "",
                            password: "",
                            api_key: "",
                        },
                    },
                },
            },
        ],
    });

    const [jsonOutput, setJsonOutput] = useState("");

    // Обработчик изменения данных
    const handleInputChange = (e, path) => {
        const { name, value } = e.target;
        const updatedData = { ...contractData };

        // Если path не задан, используем name в качестве ключа
        const keys = path ? path.split('.') : [name];

        // Создаем копию объекта, по которому будем изменять значение
        let temp = updatedData;

        // Перебираем ключи и идем по пути
        keys.slice(0, -1).forEach(key => {
            // Если на пути не существует такого объекта, создаем его
            if (!temp[key]) {
                temp[key] = {};
            }
            temp = temp[key]; // Переходим на следующий уровень
        });

        // Устанавливаем новое значение по последнему ключу
        temp[keys[keys.length - 1]] = value;

        // Обновляем состояние
        setContractData(updatedData);
    };


    // Добавление нового поля в список полей
    const handleAddField = () => {
        setContractData({
            ...contractData,
            fields: [
                ...contractData.fields,
                {
                    name: "",
                    type: "",
                    source: {
                        id: "",
                        name: "",
                        field_mapping: {
                            source_field: "",
                            target_field: "",
                        },
                        authentication: {
                            type: "",
                            credentials: {
                                username: "",
                                password: "",
                                api_key: "",
                            },
                        },
                    },
                },
            ],
        });
    };

    // Удаление поля из списка полей
    const handleRemoveField = (index) => {
        const newFields = contractData.fields.filter((_, i) => i !== index);
        setContractData({ ...contractData, fields: newFields });
    };

    // Генерация JSON-объекта
    const handleGenerateJson = () => {
        setJsonOutput(JSON.stringify(contractData, null, 2));
    };

    return (
        <div className={styles.container}>
            <h1>Contract Specification Constructor</h1>
            <div className={styles.form}>
                <h2>Contract Details</h2>
                <input
                    type="text"
                    name="contract_id"
                    value={contractData.contract_id}
                    onChange={(e) => handleInputChange(e, "contract_id")}
                    placeholder="Contract ID"
                />
                <input
                    type="text"
                    name="name"
                    value={contractData.name}
                    onChange={(e) => handleInputChange(e, "name")}
                    placeholder="Contract Name"
                />
                <textarea
                    name="description"
                    value={contractData.description}
                    onChange={(e) => handleInputChange(e, "description")}
                    placeholder="Contract Description"
                />

                <h2>Model Information</h2>
                <input
                    type="text"
                    name="model.id"
                    value={contractData.model.id}
                    onChange={(e) => handleInputChange(e, "model.id")}
                    placeholder="Model ID"
                />
                <input
                    type="text"
                    name="model.name"
                    value={contractData.model.name}
                    onChange={(e) => handleInputChange(e, "model.name")}
                    placeholder="Model Name"
                />
                <input
                    type="text"
                    name="model.version"
                    value={contractData.model.version}
                    onChange={(e) => handleInputChange(e, "model.version")}
                    placeholder="Model Version"
                />

                <h2>Fields</h2>
                {contractData.fields.map((field, index) => (
                    <div key={index} className={styles.fieldRow}>
                        <input
                            type="text"
                            name={`fields[${index}].name`}
                            value={field.name}
                            onChange={(e) => handleInputChange(e, `fields[${index}].name`)}
                            placeholder="Field Name"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].type`}
                            value={field.type}
                            onChange={(e) => handleInputChange(e, `fields[${index}].type`)}
                            placeholder="Field Type"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.id`}
                            value={field.source.id}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.id`)}
                            placeholder="Source ID"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.name`}
                            value={field.source.name}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.name`)}
                            placeholder="Source Name"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.field_mapping.source_field`}
                            value={field.source.field_mapping.source_field}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.field_mapping.source_field`)}
                            placeholder="Source Field"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.field_mapping.target_field`}
                            value={field.source.field_mapping.target_field}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.field_mapping.target_field`)}
                            placeholder="Target Field"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.authentication.type`}
                            value={field.source.authentication.type}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.authentication.type`)}
                            placeholder="Authentication Type"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.authentication.credentials.username`}
                            value={field.source.authentication.credentials.username}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.authentication.credentials.username`)}
                            placeholder="Username"
                        />
                        <input
                            type="password"
                            name={`fields[${index}].source.authentication.credentials.password`}
                            value={field.source.authentication.credentials.password}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.authentication.credentials.password`)}
                            placeholder="Password"
                        />
                        <input
                            type="text"
                            name={`fields[${index}].source.authentication.credentials.api_key`}
                            value={field.source.authentication.credentials.api_key}
                            onChange={(e) => handleInputChange(e, `fields[${index}].source.authentication.credentials.api_key`)}
                            placeholder="API Key"
                        />
                        <button
                            type="button"
                            className={styles.removeButton}
                            onClick={() => handleRemoveField(index)}
                        >
                            Remove Field
                        </button>
                    </div>
                ))}
                <button className={styles.addButton} onClick={handleAddField}>
                    Add Field
                </button>
                <button className={styles.generateButton} onClick={handleGenerateJson}>
                    Generate JSON
                </button>
            </div>

            <div className={styles.jsonOutput}>
                <h2>Generated JSON</h2>
                <pre>{jsonOutput}</pre>
            </div>
        </div>
    );
};

export default ContractConstructor;
