using DinkToPdf;
using System;
using System.IO;
using WatchmanWeb.Utility;

namespace WatchmanWeb.Services
{
    public interface IPdfService
    {
        HtmlToPdfDocument getPdf();
    }
    public class PdfService : IPdfService
    {
        private readonly IIncidentService _incidentService;
        public PdfService(IIncidentService incidentService)
        {
            _incidentService = incidentService;
        }
        public HtmlToPdfDocument getPdf()
        {
            var incidents = _incidentService.GetAll();

            var globalSettings = new GlobalSettings
            {
                ColorMode = ColorMode.Color,
                Orientation = Orientation.Portrait,
                PaperSize = PaperKind.A4,
                Margins = new MarginSettings { Top = 10 },
                DocumentTitle = "PDF Report",
            };

            var objectSettings = new ObjectSettings
            {
                PagesCount = true,
                HtmlContent = TemplateGenerator.GetHTMLString(incidents),
                WebSettings = { DefaultEncoding = "utf-8", UserStyleSheet = Path.Combine(Directory.GetCurrentDirectory(), "assets", "styles.css") },
                HeaderSettings = { FontName = "Arial", FontSize = 25, Right = "Raport Watchman, " + DateTime.Now.ToString("dd.MM.yyyy"), Line = true },
                FooterSettings = { FontName = "Arial", FontSize = 25, Line = true, Center = "WATCHMAN" }
            };

            var pdf = new HtmlToPdfDocument()
            {
                GlobalSettings = globalSettings,
                Objects = { objectSettings }
            };
            return pdf;
        }
    }
}
