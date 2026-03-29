import React from 'react';

export default function ModuleShell({ title, description, children, actions }) {
  return (
    <div className="module">
      <header className="module-header">
        <div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
        {actions ? <div className="module-header-actions">{actions}</div> : null}
      </header>
      <div className="module-content">{children}</div>
    </div>
  );
}
