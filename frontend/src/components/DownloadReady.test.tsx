import { render, screen } from '@testing-library/react'
import { DownloadReady } from './DownloadReady'

describe('DownloadReady', () => {
  it('отображает сообщение и кнопку загрузки', () => {
    render(<DownloadReady downloadUrl="blob:test-url" filename="result.jpg" />)

    expect(screen.getByText(/файл готов/i)).toBeInTheDocument()

    const button = screen.getByTestId('down-file')
    expect(button).toBeInTheDocument()
    expect(button).toHaveTextContent(/скачать готовый файл/i)

    const link = button.closest('a')
    expect(link).toHaveAttribute('href', 'blob:test-url')
    expect(link).toHaveAttribute('download', 'result.jpg')
  })
})
