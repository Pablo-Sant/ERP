import React, { useEffect, useState } from 'react';
import { getErrorMessage } from '../services/api';

function initialState(fields) {
  return fields.reduce((accumulator, field) => {
    accumulator[field.name] = field.defaultValue ?? '';
    return accumulator;
  }, {});
}

function serialize(field, value) {
  if (value === '' || value === null || value === undefined) {
    return field.required ? value : null;
  }

  if (field.type === 'number') return Number(value);
  if (field.asBoolean) return value === true || value === 'true' || value === '1';
  if (field.type === 'json') return typeof value === 'string' ? JSON.parse(value) : value;
  return value;
}

export default function EntityPanel({
  title,
  description,
  fields,
  columns,
  loadItems,
  createItem,
  deleteItem,
  getItemKey,
}) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(() => initialState(fields));
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  async function refresh() {
    try {
      setLoading(true);
      const response = await loadItems();
      setItems(response.data ?? []);
      setError('');
    } catch (loadError) {
      setError(getErrorMessage(loadError, 'Falha ao carregar dados.'));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setSaving(true);
      const payload = fields.reduce((accumulator, field) => {
        accumulator[field.name] = serialize(field, form[field.name]);
        return accumulator;
      }, {});

      await createItem(payload);
      setForm(initialState(fields));
      await refresh();
    } catch (saveError) {
      setError(getErrorMessage(saveError, 'Falha ao salvar registro.'));
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(item) {
    try {
      await deleteItem(getItemKey(item));
      await refresh();
    } catch (deleteError) {
      setError(getErrorMessage(deleteError, 'Falha ao excluir registro.'));
    }
  }

  return (
    <section className="card entity-panel">
      <div className="entity-panel-header">
        <div>
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
        <button className="btn btn-secondary" onClick={refresh} type="button">
          Atualizar
        </button>
      </div>

      {error ? <div className="alert alert-danger">{error}</div> : null}

      <form className="form-grid entity-form" onSubmit={handleSubmit}>
        {fields.map((field) => (
          <div className={`form-group ${field.fullWidth ? 'full-width' : ''}`} key={field.name}>
            <label htmlFor={`${title}-${field.name}`}>{field.label}</label>
            {field.type === 'textarea' || field.type === 'json' ? (
              <textarea
                id={`${title}-${field.name}`}
                onChange={(event) =>
                  setForm((current) => ({ ...current, [field.name]: event.target.value }))
                }
                placeholder={field.placeholder}
                required={field.required}
                rows={field.rows ?? 3}
                value={form[field.name]}
              />
            ) : (
              <input
                id={`${title}-${field.name}`}
                onChange={(event) =>
                  setForm((current) => ({ ...current, [field.name]: event.target.value }))
                }
                placeholder={field.placeholder}
                required={field.required}
                step={field.step}
                type={field.type ?? 'text'}
                value={form[field.name]}
              />
            )}
          </div>
        ))}

        <div className="form-group full-width">
          <button className="btn btn-primary" disabled={saving} type="submit">
            {saving ? 'Salvando...' : 'Adicionar registro'}
          </button>
        </div>
      </form>

      {loading ? (
        <div className="loading-inline">Carregando registros...</div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column.label}>{column.label}</th>
                ))}
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan={columns.length + 1}>Nenhum registro encontrado.</td>
                </tr>
              ) : (
                items.map((item) => (
                  <tr key={getItemKey(item)}>
                    {columns.map((column) => (
                      <td key={column.label}>
                        {column.render ? column.render(item) : item[column.key]}
                      </td>
                    ))}
                    <td>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(item)}
                        type="button"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
