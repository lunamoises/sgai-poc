import React, { useEffect, useState } from 'react'

const isRecent = (ts) => {
  if (!ts) return false
  return (Date.now() - new Date(ts).getTime()) < 5 * 60 * 1000
}

export default function App() {
  const [assets, setAssets] = useState([])
  const [loading, setLoading] = useState(true)

  const fetch_assets = () => {
    fetch('/v1/assets')
      .then(r => r.json())
      .then(d => { setAssets(d); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => {
    fetch_assets()
    const t = setInterval(fetch_assets, 30000)
    return () => clearInterval(t)
  }, [])

  return (
    <div style={{fontFamily:'sans-serif',padding:'2rem',maxWidth:'1000px',margin:'0 auto'}}>
      <h1 style={{borderBottom:'2px solid #333',paddingBottom:'0.5rem'}}>
        SGAI — Gestión de Activos v2
      </h1>
      {loading ? <p>Cargando...</p> : (
        <table style={{width:'100%',borderCollapse:'collapse'}}>
          <thead>
            <tr style={{background:'#222',color:'#fff'}}>
              {['Estado','Hostname','IP Interna','CPU','RAM','Disco libre','Último reporte'].map(h =>
                <th key={h} style={{padding:'8px',textAlign:'left'}}>{h}</th>
              )}
            </tr>
          </thead>
          <tbody>
            {assets.map((a,i) => (
              <tr key={a.id} style={{background: i%2===0?'#f9f9f9':'#fff'}}>
                <td style={{padding:'8px',textAlign:'center'}}>
                  <span style={{
                    display:'inline-block',width:'14px',height:'14px',borderRadius:'50%',
                    background: isRecent(a.ultimo_reporte) ? '#22c55e' : '#ef4444'
                  }} title={isRecent(a.ultimo_reporte)?'Activo':'Sin reporte reciente'}/>
                </td>
                <td style={{padding:'8px'}}>{a.hostname}</td>
                <td style={{padding:'8px'}}>{a.ip_interna}</td>
                <td style={{padding:'8px'}}>{a.modelo_cpu}</td>
                <td style={{padding:'8px'}}>{a.ram_total}</td>
                <td style={{padding:'8px'}}>{a.disco_libre}</td>
                <td style={{padding:'8px',fontSize:'0.85em',color:'#666'}}>
                  {a.ultimo_reporte ? new Date(a.ultimo_reporte).toLocaleString() : '—'}
                </td>
              </tr>
            ))}
            {assets.length === 0 && (
              <tr><td colSpan="7" style={{padding:'2rem',textAlign:'center',color:'#999'}}>
                Sin activos registrados. Ejecuta agent.ps1 en un equipo Windows.
              </td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  )
}
