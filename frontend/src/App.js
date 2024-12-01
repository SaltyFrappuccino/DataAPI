import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import DataSourcesPage from './pages/DataSourcesPage/DataSourcesPage';
import DataTransformationPage from "./pages/DataTransformationPage/DataTransformationPage";
import ContractsRegexPage from "./pages/ContractsRegexPage/ContractsRegexPage";
import ModelsPage from "./pages/ModelsPage/ModelsPage";
import './App.css'
import ContractConstructorPage from "./pages/ContractConstructorPage/ContractConstructorPage";
import WorkflowPage from "./pages/Workflow/WorkflowPage";

const App = () => {
    return (
        <Router>
            <div style={{ display: 'flex' }}>
                {/* Navbar всегда отображается слева */}
                <Navbar />
                {/* Основной контент справа от Navbar */}
                <div style={{ marginLeft: '250px', flex: 1, padding: '20px' }}>
                    <Routes>
                        <Route path="/contracts" element={<ContractsRegexPage/>} />
                        <Route path="/data-sources" element={<DataSourcesPage />} />
                        <Route path="/transformers" element={<DataTransformationPage/>} />
                        <Route path="/models" element={<ModelsPage/>} />
                        <Route path="/monitoring" element={<h1>Мониторинг</h1>} />
                        <Route path="/logging" element={<h1>Логгирование</h1>} />
                        <Route path="/contract-constructor" element={<ContractConstructorPage/>} />
                        <Route path="/workflow/:name" element={<WorkflowPage/>} />
                        {/* Добавляем редирект на /data-sources для корневого пути */}
                        <Route path="/" element={<Navigate to="/data-sources" />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;
