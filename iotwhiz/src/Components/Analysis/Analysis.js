import React from 'react';
import './Analysis.css';

const Analysis = ({ genericAnalysis, layoutAnalysis }) => {
  if (!genericAnalysis || !layoutAnalysis) {
    return <div>Loading...</div>;
  }

  const accordionItems = [
    {
      title: `Detected APIs (${genericAnalysis.total_usages})`,
      content: (
        <ul>
          {genericAnalysis.detected_apis.map((api, index) => (
            <li key={index}>{api}</li>
          ))}
        </ul>
      ),
      total: genericAnalysis.total_usages,
    },
    {
      title: `Detected Dynamic Loading (${genericAnalysis.total_dynamic_usages})`,
      content: (
        <ul>
          {genericAnalysis.detected_dynamic_loading.map((dynamic, index) => (
            <li key={index}>{dynamic}</li>
          ))}
        </ul>
      ),
      total: genericAnalysis.total_dynamic_usages,
    },
    {
      title: `Detected Permissions (${genericAnalysis.total_permissions})`,
      content: (
        <ul>
          {genericAnalysis.detected_permissions.map((permission, index) => (
            <li key={index}>{permission}</li>
          ))}
        </ul>
      ),
      total: genericAnalysis.total_permissions,
    },
    {
      title: 'Widgets and Views',
      content: (
        <ul>
          {layoutAnalysis.Widgets_and_Views.map((widget, index) => (
            <li key={index}>
              <span>Widget or View Path:</span> {widget[0]}
              <span>Count:</span> {widget[1]}
              <span>Widget Type:</span> {widget[2]}
            </li>
          ))}
        </ul>
      ),
    },
    {
      title: 'Layout Types',
      content: (
        <ul>
          {layoutAnalysis.Layout_Types.map((layoutType, index) => (
            <li key={index}>{layoutType}</li>
          ))}
        </ul>
      ),
    },
    {
      title: 'Nested Layouts',
      content: (
        <ul>
          {layoutAnalysis.Nested_Layouts.map((nestedLayout, index) => (
            <li key={index}>{nestedLayout}</li>
          ))}
        </ul>
      ),
    },
  ];

  return (
    <div className="analysis-container">
      {accordionItems.map((item, index) => (
        <div className="accordion" id={`accordion-${index + 1}`}>
          <h2 className="accordion-header" id={`heading-${index + 1}`}>
            <button
              className="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target={`#collapse-${index + 1}`}
              aria-controls={`collapse-${index + 1}`}
            >
              {item.title}
            </button>
          </h2>
          <div
            id={`collapse-${index + 1}`}
            className="accordion-collapse collapse"
            aria-labelledby={`heading-${index + 1}`}
            data-bs-parent={`#accordion-${index + 1}`}
          >
            <div className="accordion-body">
              {item.content}
              {item.total && <p>Total: {item.total}</p>}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Analysis;
