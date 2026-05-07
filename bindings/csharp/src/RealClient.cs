using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Phenotype.MCP;

/// <summary>
/// Real C# MCP client with HttpClient
/// </summary>
public class RealMCPClient : IDisposable
{
    private readonly HttpClient _http;
    private readonly string _endpoint;
    private string? _sessionId;

    public RealMCPClient(string endpoint)
    {
        _endpoint = endpoint;
        _http = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(30)
        };
    }

    /// <summary>Initialize with MCP server</summary>
    public async Task<ServerInfo> InitializeAsync()
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = Guid.NewGuid().ToString(),
            Method = "initialize",
            Params = new Dictionary<string, object>
            {
                ["protocolVersion"] = "2024-11-05",
                ["capabilities"] = new Dictionary<string, object>(),
                ["clientInfo"] = new Dictionary<string, string>
                {
                    ["name"] = "pheno-csharp",
                    ["version"] = "0.1.0"
                }
            }
        };

        var response = await SendAsync<InitializeResponse>(request);
        _sessionId = Guid.NewGuid().ToString();
        return response.Result!.ServerInfo;
    }

    /// <summary>List available tools</summary>
    public async Task<List<McpTool>> ListToolsAsync()
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = Guid.NewGuid().ToString(),
            Method = "tools/list"
        };

        var response = await SendAsync<ToolsListResponse>(request);
        return response.Result?.Tools ?? new List<McpTool>();
    }

    /// <summary>Call a tool</summary>
    public async Task<ToolResult> CallToolAsync(string name, Dictionary<string, object> args)
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = Guid.NewGuid().ToString(),
            Method = "tools/call",
            Params = new Dictionary<string, object>
            {
                ["name"] = name,
                ["arguments"] = args
            }
        };

        var response = await SendAsync<ToolCallResponse>(request);
        return response.Result!.Content.First();
    }

    private async Task<T> SendAsync<T>(JsonRpcRequest request) where T : class
    {
        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        var httpResponse = await _http.PostAsync(_endpoint, content);
        var responseJson = await httpResponse.Content.ReadAsStringAsync();
        
        return JsonSerializer.Deserialize<T>(responseJson)!;
    }

    public void Dispose()
    {
        _http.Dispose();
    }
}

// Request/Response types
public class JsonRpcRequest
{
    [JsonPropertyName("jsonrpc")] public string JsonRpc { get; set; } = "2.0";
    [JsonPropertyName("id")] public string Id { get; set; } = "";
    [JsonPropertyName("method")] public string Method { get; set; } = "";
    [JsonPropertyName("params")] public object? Params { get; set; }
}

public class JsonRpcResponse<T> where T : class
{
    [JsonPropertyName("jsonrpc")] public string JsonRpc { get; set; } = "";
    [JsonPropertyName("id")] public string? Id { get; set; }
    [JsonPropertyName("result")] public T? Result { get; set; }
    [JsonPropertyName("error")] public JsonRpcError? Error { get; set; }
}

public class JsonRpcError
{
    [JsonPropertyName("code")] public int Code { get; set; }
    [JsonPropertyName("message")] public string Message { get; set; } = "";
}

public class InitializeResponse
{
    [JsonPropertyName("result")] public InitializeResult? Result { get; set; }
}

public class InitializeResult
{
    [JsonPropertyName("serverInfo")] public ServerInfo ServerInfo { get; set; } = new();
}

public class ServerInfo
{
    [JsonPropertyName("name")] public string Name { get; set; } = "";
    [JsonPropertyName("version")] public string Version { get; set; } = "";
}

public class ToolsListResponse
{
    [JsonPropertyName("result")] public ToolsListResult? Result { get; set; }
}

public class ToolsListResult
{
    [JsonPropertyName("tools")] public List<McpTool> Tools { get; set; } = new();
}

public class McpTool
{
    [JsonPropertyName("name")] public string Name { get; set; } = "";
    [JsonPropertyName("description")] public string Description { get; set; } = "";
}

public class ToolCallResponse
{
    [JsonPropertyName("result")] public ToolCallResult? Result { get; set; }
}

public class ToolCallResult
{
    [JsonPropertyName("content")] public List<ToolResult> Content { get; set; } = new();
}

public class ToolResult
{
    [JsonPropertyName("type")] public string Type { get; set; } = "";
    [JsonPropertyName("text")] public string? Text { get; set; }
}
