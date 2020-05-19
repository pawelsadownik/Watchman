using Microsoft.Extensions.Logging;
using WatchmanWeb.Model;

namespace WatchmanWeb.Repositories
{
    public interface IUserRepository : IRepository<User>
    {
    }
    public class UserRepository : BaseRepository<User>, IUserRepository
    {
        public UserRepository(ApplicationDbContext applicationDbContext, ILogger<UserRepository> logger) : base(applicationDbContext, logger)
        {
        }
    }
}
