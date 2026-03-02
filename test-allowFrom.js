const fs = require('fs');
const path = require('path');

// 读取 store 文件
const storePath = path.join(process.env.HOME, '.openclaw/credentials/feishu-default-allowFrom.json');
console.log('Store path:', storePath);

try {
  const content = fs.readFileSync(storePath, 'utf8');
  console.log('File content:', content);
  
  const data = JSON.parse(content);
  console.log('Parsed data:', JSON.stringify(data, null, 2));
  
  if (data.allowFrom && Array.isArray(data.allowFrom)) {
    console.log('allowFrom entries:', data.allowFrom);
    data.allowFrom.forEach((entry, i) => {
      console.log(`  Entry ${i}: "${entry}" (lowercase: "${entry.toLowerCase()}")`);
    });
  }
} catch (err) {
  console.error('Error reading file:', err);
}
