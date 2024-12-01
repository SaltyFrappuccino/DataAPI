import React, { useRef, useState, useCallback, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  ReactFlow,
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
} from "@xyflow/react";
import ModalForm from "../../components/ModalForm/ModalForm";
import "@xyflow/react/dist/style.css";
import "./styles.css";


const Sidebar = ({ fields, operations, onDragStart }) => (
  <aside className="sidebar">
    <h2>Nodes</h2>
    <div className="node-group">
      <h3>Fields</h3>
      {fields.map((field) => (
        <div
          key={field.name}
          className="dndnode field-node"
          onDragStart={(event) => onDragStart(event, field.name, "field")}
          draggable
        >
          {field.name}
        </div>
      ))}
    </div>
    <div className="node-group">
      <h3>Operations</h3>
      {Object.keys(operations).map((operation) => (
        <div
          key={operation}
          className="dndnode operation-node"
          onDragStart={(event) => onDragStart(event, operation, "operation")}
          draggable
        >
          {operation}
        </div>
      ))}
    </div>
  </aside>
);

const WorkflowPage = () => {
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([
    {
      id: "start",
      type: "input",
      position: { x: 250, y: 5 },
      data: { label: "Start Node" },
    },
  ]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [fields, setFields] = useState([]);
  const [operations, setOperations] = useState({});
  const [dragType, setDragType] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [generatedJSON, setGeneratedJSON] = useState(null);
  const { name } = useParams();

  useEffect(() => {
    const fetchConfig = async () => {
      const response = await fetch("http://127.0.0.1:8002/contracts");
      const data = await response.json();
      const contract = data.find((c) => c.name === name);
      setFields(contract.data.model.input_requirements.features);
      setOperations({
        range_check: {
          description: "Range Check",
          parameters: { min: "Min", max: "Max" },
        },
        math_function: {
          description: "Math Function",
          parameters: { function: "Function", base: "Base" },
        },
        filter: {
          description: "Value Filter",
          parameters: { condition: "Condition" },
        },
        custom_operation: {
          description: "Custom Operation",
          parameters: { formula: "Formula", output_type: "Output Type" },
        },
      });
    };
    fetchConfig();
  }, [name]);

  const onDragStart = (event, nodeName, type) => {
    setDragType({ name: nodeName, type });
    event.dataTransfer.effectAllowed = "move";
  };

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const position = reactFlowWrapper.current.getBoundingClientRect();
      const newNode = {
        id: `${dragType.name}_${Date.now()}`,
        type: dragType.type,
        position: {
          x: event.clientX - position.left,
          y: event.clientY - position.top,
        },
        data: {
          label: dragType.name,
          parameters: dragType.type === "operation" ? operations[dragType.name]?.parameters : null,
        },
      };
      setNodes((nds) => nds.concat(newNode));
    },
    [dragType, setNodes, operations]
  );

  const generateJSON = () => {
    const connectedNodes = new Set(["start"]);
    edges.forEach(({ source, target }) => {
      if (connectedNodes.has(source)) {
        connectedNodes.add(target);
      }
    });
    const result = nodes
      .filter((node) => connectedNodes.has(node.id))
      .map((node) => ({
        id: node.id,
        label: node.data.label,
        parameters: node.data.parameters || null,
      }));
    setGeneratedJSON(result);
    setIsModalOpen(true);
  };

  const updateNodeParameters = (key, value) => {
    setNodes((nds) => {
      const updatedNodes = nds.map((node) =>
        node.id === selectedNode.id
          ? {
              ...node,
              data: {
                ...node.data,
                parameters: {
                  ...node.data.parameters,
                  [key]: value,
                },
              },
            }
          : node
      );

      // Обновляем selectedNode, чтобы отразить изменения
      const updatedSelectedNode = updatedNodes.find((node) => node.id === selectedNode.id);
      setSelectedNode(updatedSelectedNode);

      return updatedNodes;
    });
  };

  return (
    <div className="dndflow">
      <div className="reactflow-wrapper" ref={reactFlowWrapper}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={(params) => setEdges((eds) => addEdge(params, eds))}
          onDrop={onDrop}
          onDragOver={(event) => event.preventDefault()}
          onNodeClick={(event, node) => setSelectedNode(node)}
          fitView
        >
          <Controls />
          <Background />
        </ReactFlow>
        {selectedNode && (
          <div className="node-editor">
            <h3>Edit Node: {selectedNode.data.label}</h3>
            {selectedNode.data.parameters &&
              Object.keys(selectedNode.data.parameters).map((key) => (
                <div key={key}>
                  <label>{key}: </label>
                  <input
                    type="text"
                    value={selectedNode.data.parameters[key]}
                    onChange={(e) => updateNodeParameters(key, e.target.value)}
                  />
                </div>
              ))}
          </div>
        )}
        <button className="generate-button" onClick={generateJSON}>
          Generate JSON
        </button>
      </div>
      <Sidebar fields={fields} operations={operations} onDragStart={onDragStart} />
      <ModalForm isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <h3>Generated JSON</h3>
        <pre>{JSON.stringify(generatedJSON, null, 2)}</pre>
      </ModalForm>
    </div>
  );
};

export default () => (
  <ReactFlowProvider>
    <WorkflowPage />
  </ReactFlowProvider>
);
