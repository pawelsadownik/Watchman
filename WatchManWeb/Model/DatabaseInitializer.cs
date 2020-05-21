using Microsoft.Extensions.Configuration;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.Model
{
    public interface IDatabaseInitializer
    {
        Task SeedAsync();
    }
    public class DatabaseInitializer : IDatabaseInitializer
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _config;

        public DatabaseInitializer(ApplicationDbContext context, IConfiguration config)
        {
            _context = context;
            _config = config;
        }

        public async Task SeedAsync()
        {
            await SeedUSers();
            await SeedIncidents();
        }

        public async Task SeedUSers()
        {
            if (!_context.Users.Any(user => user.UserType.Equals("Admin")))
            {
                await _context.Users.AddAsync(new User()
                {
                    Id = new Guid(),
                    UserName = "admin",
                    FirstName = "admin",
                    Password = _config["AdminPassword:password"],
                    UserType = "Admin"
                });

                await _context.SaveChangesAsync();
            }
        }

        public async Task SeedIncidents()
        {
            if (!_context.Incidents.Any())
            {
                await _context.Incidents.AddRangeAsync(new Incident()
                {
                    Id = new Guid(),
                    Flag = "red",
                    Timestampt = DateTime.Now,
                    CameraInfo = "Cam1"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "yellow",
                    Timestampt = DateTime.Now.AddDays(-1),
                    CameraInfo = "Cam1"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "red",
                    Timestampt = DateTime.Now.AddDays(-2),
                    CameraInfo = "Cam2"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "yellow",
                    Timestampt = DateTime.Now.AddDays(-3),
                    CameraInfo = "Cam2"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "red",
                    Timestampt = DateTime.Now.AddDays(-4),
                    CameraInfo = "Cam3"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "yellow",
                    Timestampt = DateTime.Now.AddDays(-5),
                    CameraInfo = "Cam3"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "red",
                    Timestampt = DateTime.Now.AddDays(-6),
                    CameraInfo = "Cam4"
                }, new Incident()
                {
                    Id = new Guid(),
                    Flag = "yellow",
                    Timestampt = DateTime.Now.AddDays(-7),
                    CameraInfo = "Cam4"
                }
                );

                await _context.SaveChangesAsync();
            }
        }
    }
}
