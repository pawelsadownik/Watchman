using System;
using System.Collections.Generic;
using System.Linq;
using WatchmanWeb.Model;
using WatchmanWeb.Repositories;

namespace WatchmanWeb.Services
{
    public interface IUserService: IService<User>
    {

    }
    public class UserService : IUserService
    {
        private readonly IUserRepository _UserRepository;
        private readonly ApplicationDbContext _applicationDbContext;

        public UserService(IUserRepository UserRepository, ApplicationDbContext applicationDbContext)
        {
            _UserRepository = UserRepository;
            _applicationDbContext = applicationDbContext;
        }

        public void Add(User entity)
        {
            _UserRepository.Add(entity);
            _applicationDbContext.SaveChanges();
        }

        public List<User> GetAll()
        {
            return _UserRepository.GetAll().ToList();
        }

        public User GetById(Guid id)
        {
            return _UserRepository.GetById(id).SingleOrDefault();
        }

        public void Remove(Guid id)
        {
            _UserRepository.Remove(id);
            _applicationDbContext.SaveChanges();
        }

        public void Update(User entity)
        {
            _UserRepository.Update(entity);
            _applicationDbContext.SaveChanges();
        }
    }
}
