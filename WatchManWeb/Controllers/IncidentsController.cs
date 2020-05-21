using AutoMapper;
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
        private readonly IMapper _mapper;
        public IncidentsController(IIncidentService incidentService, IMapper mapper)
        {
            _incidentService = incidentService;
            _mapper = mapper;
        }

        [HttpGet]
        public List<IncidentVM> GetAll()
        {
            return _mapper.Map<List<IncidentVM>>(_incidentService.GetAll());
        }

        [HttpGet("{id}")]
        public IncidentVM GetById(Guid id)
        {
            var incident = _incidentService.GetById(id);
            return _mapper.Map<IncidentVM>(incident);
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] IncidentVM incidentVM)
        {
            var incident = _mapper.Map<Incident>(incidentVM);

            _incidentService.Add(incident);
            return Created("/api/Incident", _mapper.Map<IncidentVM>(incident).Id);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            _incidentService.Remove(id);
            return Ok();
        }

        [HttpPut]
        public async Task<IActionResult> Update([FromBody] IncidentVM incidentVM)
        {
            if (incidentVM == null)
            {
                return BadRequest();
            }
            _incidentService.Update(_mapper.Map<Incident>(incidentVM));
            return Ok();
        }
    }
}
