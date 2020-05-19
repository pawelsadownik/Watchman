using System;
using System.Collections.Generic;

namespace WatchmanWeb.Services
{
    public interface IService<TEntity>
    {
        List<TEntity> GetAll();
        void Add(TEntity entity);
        void Remove(Guid id);
        void Update(TEntity entity);
        TEntity GetById(Guid id);

    }
}
