import React from 'react'

interface FilePickerProps {
    onFileSelect: (file: File) => void
}

export const FilePicker: React.FC<FilePickerProps> = ({ onFileSelect }) => {
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (file) {
            onFileSelect(file)
        }
    }

    return (
        <div className="file_picker">
            <input className="input-file" type="file" name='image' onChange={handleChange} />
        </div>
    )
}