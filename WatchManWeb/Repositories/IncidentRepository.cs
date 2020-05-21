using Microsoft.Extensions.Logging;
using WatchmanWeb.Model;

namespace WatchmanWeb.Repositories
{
    public interface IIncidentRepository : IRepository<Incident>
    {
    }
    public class IncidentRepository : BaseRepository<Incident>, IIncidentRepository
    {
        public IncidentRepository(ApplicationDbContext applicationDbContext, ILogger<IncidentRepository> logger) : base(applicationDbContext, logger)
        {
        }
    }
}
