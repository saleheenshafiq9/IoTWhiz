import React, { useState, useEffect } from 'react';
import './Analysis.css';

const Modal = ({ closeModal, children }) => (
  <div className="modal-overlay">
      <span className="close" onClick={closeModal}>
        &times;
      </span>
    <div className="modal-analysis">
      {children}
    </div>
  </div>
);

const Analysis = ({ genericAnalysis, layoutAnalysis }) => {
  const [modalContent, setModalContent] = useState(null);

  useEffect(() => {
    if (!genericAnalysis || !layoutAnalysis) {
      setModalContent(<div>Loading...</div>);
    }
  }, [genericAnalysis, layoutAnalysis]);

  const openModal = (content) => {
    setModalContent(content);
  };

  const closeModal = () => {
    setModalContent(null);
  };
  
  const cardItems = [
    {
      title: `Detected APIs`,
      usage: genericAnalysis.total_usages,
      content: (
        <ul>
          {genericAnalysis.detected_apis.map((api, index) => {
            const parts = api.split(':');
            const filePath = parts[0];
            const lineNumber = parts[1];
            const code = parts.slice(2).join(':'); // Concatenate remaining parts with ':'
            return (
              <li key={index}>
                <span className="index">{index + 1}:</span>{' '}
                <span className="filePath">{filePath}:</span>
                <span className="lineNumber">{lineNumber}:</span> <br />
                <span className="code">{code}</span>
              </li>
            );
          })}
        </ul>
      ),
      total: genericAnalysis.total_usages,
    },
    {
      title: `Detected Dynamic Loading`,
      usage: genericAnalysis.total_dynamic_usages,
      content: (
        <ul>
          {genericAnalysis.detected_dynamic_loading.map((dynamic, index) => {
            const parts = dynamic.split(':');
            const filePath = parts[0];
            const lineNumber = parts[1];
            const code = parts.slice(2).join(':'); // Concatenate remaining parts with ':'
            return (
              <li key={index}>
                <span className="index">{index + 1}:</span>{' '}
                <span className="filePath">{filePath}:</span>
                <span className="lineNumber">{lineNumber}:</span> <br />
                <span className="code">{code}</span>
              </li>
            );
          })}
        </ul>
      ),
      total: genericAnalysis.total_dynamic_usages,
    },
    {
      title: `Detected Permissions`,
      usage: genericAnalysis.total_permissions,
      content: (
        <ul>
          {genericAnalysis.detected_permissions.map((permission, index) => {
            const firstColonIndex = permission.indexOf(':');
            const secondColonIndex = permission.indexOf(':', firstColonIndex + 1);
            
            const filePath = permission.substring(0, firstColonIndex);
            const lineNumber = permission.substring(firstColonIndex + 1, secondColonIndex);
            const code = permission.substring(secondColonIndex + 1);
    
            return (
              <li key={index}>
                <span className="index">{index + 1}:</span>{' '}
                <span className="filePath">{filePath}:</span>
                <span className="lineNumber">{lineNumber}:</span> <br />
                <span className="code">{code}</span>
              </li>
            );
          })}
        </ul>
      ),
      total: genericAnalysis.total_permissions,
    },      
    {
      title: 'Widgets and Views',
      content: (
        <ul>
          {layoutAnalysis.Widgets_and_Views.map((widget, index) => (
            <li key={index} style={{
              color: "#333"
            }}>
              <span className="filePath">Widget or View Path:</span> {widget[0]} <br />
              <span className="count">Count:</span> {widget[1]} <br />
              <span className="widgetType">Widget Type:</span> {widget[2]} <br />
            </li>
          ))}
        </ul>
      ),
    },    
    {
      title: 'Layout Types',
      content: (
        <ul>
          {layoutAnalysis.Layout_Types.map((layoutType, index) => {
            if (Array.isArray(layoutType) && layoutType.length === 2) {
              const [layout, filePath] = layoutType;
              return (
                <li key={index} style={{
                  color: "#333"
                }}>
                  <span className="layoutType">Layout Type:</span> {layout} <br />
                  <span className="filePath">File Path:</span> {filePath}
                </li>
              );
            }
            return null;
          })}
        </ul>
      ),
    },    
    {
      title: 'Nested Layouts',
      content: (
        <ul>
          {layoutAnalysis.Nested_Layouts.map((nestedLayout, index) => {
            if (Array.isArray(nestedLayout) && nestedLayout.length === 2) {
              const [filePath, layoutContent] = nestedLayout;
              return (
                <li key={index} style={{
                  color: "#333"
                }}>
                  <span className="filePath">File Path:</span> {filePath} <br />
                  <span className="layoutContent">Layout Content:</span> {layoutContent}
                </li>
              );
            }
            return null;
          })}
        </ul>
      ),
    }    
  ];

 return (
    <div className="analysis-container">
      {cardItems.map((item, index) => (
        <div className="card" key={index} onClick={() => openModal(item.content)}>
          <div className="card-header">
            {item.title}
          </div>
          {item.usage && <div className='usage'>{item.usage}</div>}
        </div>
      ))}

      {modalContent && <Modal closeModal={closeModal}>{modalContent}</Modal>}
    </div>
  );
};

export default Analysis;