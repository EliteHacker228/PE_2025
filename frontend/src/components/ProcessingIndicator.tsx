import React from 'react'
import './ProcessingIndicator.css'

export const ProcessingIndicator: React.FC = () => {
  return (
    <div className="processing-wrapper">
      <div className="loader"></div>
      <p>Идёт обработка файла...</p>
    </div>
  )
}
