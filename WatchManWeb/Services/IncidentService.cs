using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WatchmanWeb.Model;
using WatchmanWeb.Repositories;

namespace WatchmanWeb.Services
{
    public interface IIncidentService : IService<Incident>
    {

    }
    public class IncidentService : IIncidentService
    {
        private readonly IIncidentRepository _incidentRepository;
        private readonly ApplicationDbContext _applicationDbContext;

        public IncidentService(IIncidentRepository incidentRepository, ApplicationDbContext applicationDbContext)
        {
            _incidentRepository = incidentRepository;
            _applicationDbContext = applicationDbContext;
        }

        public void Add(Incident entity)
        {
            _incidentRepository.Add(entity);
            _applicationDbContext.SaveChanges();
        }

        public List<Incident> GetAll()
        {
            return _incidentRepository.GetAll().ToList();
        }

        public Incident GetById(Guid id)
        {
            return _incidentRepository.GetById(id).SingleOrDefault();
        }

        public void Remove(Guid id)
        {
            _incidentRepository.Remove(id);
            _applicationDbContext.SaveChanges();
        }

        public void Update(Incident entity)
        {
            _incidentRepository.Update(entity);
            _applicationDbContext.SaveChanges();
        }
    }
}
