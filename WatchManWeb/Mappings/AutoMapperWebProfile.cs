using AutoMapper;
using System;
using WatchmanWeb.Model;
using WatchmanWeb.ViewModel;

namespace WatchmanWeb.Mappings
{
    public class AutoMapperWebProfile : Profile
    {
        public AutoMapperWebProfile()
        {
            CreateMap<Guid?, Guid>().ConvertUsing((src, dest) => src ?? Guid.Empty);
            CreateMap<bool?, bool>().ConvertUsing((src, dest) => src ?? false);

            CreateMap<User, UserVM>();
            CreateMap<UserVM, User>();
        }
    }
}
