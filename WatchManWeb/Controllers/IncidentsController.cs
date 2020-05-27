using AutoMapper;
using DinkToPdf.Contracts;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using WatchmanWeb.Model;
using WatchmanWeb.Services;
using WatchmanWeb.ViewModel;

namespace WatchmanWeb.Controllers
{
    [Route("api/[controller]")]
    public class IncidentsController : Microsoft.AspNetCore.Mvc.Controller
    {
        private readonly IIncidentService _incidentService;
        private readonly IPdfService _pdfService;
        private readonly IMapper _mapper;
        private IConverter _converter;

        public IncidentsController(IIncidentService incidentService, 
            IMapper mapper, IConverter converter, IPdfService pdfService)
        {
            _incidentService = incidentService;
            _mapper = mapper;
            _converter = converter;
            _pdfService = pdfService;
        }

        [HttpGet]
        public List<IncidentVM> GetAll()
        {
            return _mapper.Map<List<IncidentVM>>(_incidentService.GetAll());
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] IncidentVM incidentVM)
        {
            var incident = _mapper.Map<Incident>(incidentVM);

            _incidentService.Add(incident);
            return Created("/api/Incident", _mapper.Map<IncidentVM>(incident).Id);
        }


        [HttpGet("pdfcreator")]
        public IActionResult CreatePDF()
        {
            var pdf = _pdfService.getPdf();

            var file = _converter.Convert(pdf);
            var reportName = "Raport nr " + DateTime.Now.ToString("dd.MM.yyyy") + "-" + DateTime.Now.Millisecond + ".pdf";

            return File(file, "application/pdf", reportName);
        }
    }
}
