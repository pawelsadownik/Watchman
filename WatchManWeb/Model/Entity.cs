using Newtonsoft.Json;
using System;

namespace WatchmanWeb.Model
{
    public class Entity
    {
        public Guid Id { get; set; }
        [JsonIgnore]
        public DateTime UpdatedDate { get; set; }
        [JsonIgnore]
        public DateTime CreatedDate { get; set; }
    }
}
