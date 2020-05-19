using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WatchmanWeb.Model;

namespace WatchmanWeb.Repositories
{
    public interface IRepository<TEntity>
    {
        IQueryable<TEntity> GetAll();
        IQueryable<TEntity> GetById(Guid id);
        void Add(TEntity entity);
        void AddRange(IEnumerable<TEntity> entities);
        void Remove(Guid id);
        void RemoveRange(IEnumerable<TEntity> entities);
        void Update(TEntity entity);
    }
    public abstract class BaseRepository<T> : IRepository<T> where T : Entity
    {
        protected readonly ILogger<IRepository<T>> _logger;
        protected readonly DbSet<T> _entityDbSet;
        protected readonly ApplicationDbContext _applicationDbContext;
        protected BaseRepository(ApplicationDbContext applicationDbContext, ILogger<IRepository<T>> logger)
        {
            _applicationDbContext = applicationDbContext;
            _logger = logger;
            _entityDbSet = _applicationDbContext.Set<T>();
        }

        public IQueryable<T> GetAll()
        {
            return _entityDbSet.AsQueryable();
        }

        public void Add(T entity)
        {
            _entityDbSet.Add(entity);
        }

        public void AddRange(IEnumerable<T> entities)
        {
            _entityDbSet.AddRange(entities);
        }

        public IQueryable<T> GetById(Guid id)
        {
            return _entityDbSet.Where(x => x.Id == id);
        }

        public void Remove(Guid id)
        {
            var objectToDelete = _entityDbSet.SingleOrDefault(e => e.Id == id);
            if (objectToDelete != null)
            {
                _entityDbSet.Remove(objectToDelete);
            }
            else
            {
                _logger.LogDebug("There is no object with designated ID");
                throw new InvalidOperationException("There is no object with designated ID");
            }
        }

        public void RemoveRange(IEnumerable<T> entities)
        {
            _entityDbSet.RemoveRange(entities);
        }

        public void Update(T entity)
        {
            var itemExistInDb = _entityDbSet.Any(x => x.Id == entity.Id);
            if (itemExistInDb)
            {
                _entityDbSet.Update(entity);
            }
            else
            {
                _logger.LogDebug("There is no object with designated ID");
                throw new InvalidOperationException("There is no object with designated ID");
            }
        }
    }
}
