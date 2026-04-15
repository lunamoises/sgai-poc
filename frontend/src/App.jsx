import React,{useEffect,useState} from 'react'
export default function App(){
  const [activos,setActivos]=useState([])
  useEffect(()=>{fetch('/api/v1/activos').then(r=>r.json()).then(setActivos)},[])
  return(<div style={{fontFamily:'sans-serif',padding:'2rem'}}>
    <h1>SGAI — Gestión de Activos</h1>
    <table border="1" cellPadding="8"><thead><tr><th>ID</th><th>Nombre</th><th>Código</th><th>Categoría</th><th>Estado</th></tr></thead>
    <tbody>{activos.map(a=><tr key={a.id}><td>{a.id}</td><td>{a.nombre}</td><td>{a.codigo}</td><td>{a.categoria}</td><td>{a.estado}</td></tr>)}</tbody>
    </table></div>)
}
