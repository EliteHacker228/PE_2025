import { render, screen, fireEvent } from '@testing-library/react'
import { FilePicker } from './FilePicker'
import { vi } from 'vitest'

describe('FilePicker', () => {
  it('рендерит кнопку и скрытый input', () => {
    render(<FilePicker onFileSelect={() => {}} />)

    expect(screen.getByRole('button', { name: /выбрать файл/i })).toBeInTheDocument()
    expect(screen.getByTestId('file-input')).toBeInTheDocument()
  })

  it('при выборе файла вызывает onFileSelect и отображает имя файла', () => {
    const mockHandler = vi.fn()
    render(<FilePicker onFileSelect={mockHandler} />)

    const file = new File(['hello'], 'example.jpg', { type: 'image/jpeg' })
    const input = screen.getByTestId('file-input')

    fireEvent.change(input, { target: { files: [file] } })

    expect(mockHandler).toHaveBeenCalledWith(file)
    expect(screen.getByText(/выбран файл/i)).toBeInTheDocument()
    expect(screen.getByText('example.jpg')).toBeInTheDocument()
  })

  it('кнопка "Выбрать файл" вызывает клик по скрытому input', () => {
    render(<FilePicker onFileSelect={() => {}} />)

    const input = screen.getByTestId('file-input')
    const spy = vi.spyOn(input, 'click')

    const button = screen.getByRole('button', { name: /выбрать файл/i })
    fireEvent.click(button)

    expect(spy).toHaveBeenCalled()
  })
})
