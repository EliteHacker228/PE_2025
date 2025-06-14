import React, { useRef, useState } from 'react'

interface FilePickerProps {
  onFileSelect: (file: File) => void
}

export const FilePicker: React.FC<FilePickerProps> = ({ onFileSelect }) => {
  const inputRef = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState<string | null>(null)

  const handleButtonClick = () => {
    inputRef.current?.click()
  }

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      onFileSelect(file)
      setFileName(file.name)
    }
  }

  return (
    <div className="file-picker">
      <button type="button" className="file-button pick-button" onClick={handleButtonClick}>
        Выбрать файл
      </button>
      <input
        type="file"
        ref={inputRef}
        onChange={handleChange}
        accept="image/*"
        style={{ display: 'none' }}
        data-testid="file-input"
      />
      {fileName && (
        <p className="file-name">Выбран файл: <strong>{fileName}</strong></p>
      )}
    </div>
  )
}
