using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
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
            if (!_context.Users.Any(user => user.UserType.Equals("admin")))
            {
                await _context.Users.AddAsync(new User()
                {
                    Id = new Guid(),
                    UserName = "admin",
                    FirstName = "admin",
                    Password = _config["AdminPassword:password"],
                    UserType = "admin"
                });
                await _context.SaveChangesAsync();

            }
        }
    }
}
