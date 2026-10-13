// Portable single-file build for opening the game without an asset directory.
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8').replace(/assets\/portraits\/[a-z]+\.png/g,file=>'data:image/png;base64,'+fs.readFileSync(path.join(root,file)).toString('base64'));
fs.writeFileSync(path.join(root,'conurbano-fighter.html'),html);
console.log('Built conurbano-fighter.html');
